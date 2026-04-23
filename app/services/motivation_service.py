from app.extensions import SessionLocal
from app.models.motivation import Motivation
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

def create_motivations(theme: str, total: int):
    session = SessionLocal()

    try:
        # 🔥 PROMPT KITA UBAH MENJADI TEMA LORD OF THE MYSTERIES
        prompt = f"""
        Kamu adalah dewa kuno dari dunia Lord of the Mysteries.
        Dalam format JSON, racik {total} deskripsi Pathway (Jalur Kekuatan Beyonder) rahasia yang berkaitan dengan domain/tema "{theme}".
        
        Untuk setiap Pathway, jelaskan:
        1. Nama Pathway
        2. Kutukan/Kegilaan Fatal (Flaw)
        3. Kekuatan untuk Sequence 9 hingga Sequence 7.
        Gunakan bahasa Indonesia yang puitis, gelap, dan misterius.

        WAJIB gunakan struktur JSON murni di bawah ini agar sistem saya bisa membacanya:
        {{
            "motivations": [
                {{"text": "Tuliskan cerita Pathway pertama secara panjang lebar di sini..."}}
            ]
        }}
        """

        result = generate_from_llm(prompt)
        motivations = parse_llm_response(result)

        # save request log
        req_log = RequestLog(theme=theme)
        session.add(req_log)
        session.commit()

        saved = []

        for item in motivations:
            text = item.get("text")

            m = Motivation(
                text=text,
                request_id=req_log.id
            )
            session.add(m)
            saved.append(text)

        session.commit()

        return saved

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def get_all_motivations(page: int = 1, per_page: int = 100):
    session = SessionLocal()

    try:
        query = session.query(Motivation)

        total = query.count()

        data = (
            query
            .order_by(Motivation.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        result = [
            {
                "id": m.id,
                "text": m.text,
                "created_at": m.created_at.isoformat()
            }
            for m in data
        ]

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "data": result
        }

    finally:
        session.close()