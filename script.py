from whop_sdk import Whop

# =========================
# CONFIG (TU DONNES JUSTE ÇA)
# =========================
API_KEY    = "apik_FxgXfjyUia4rW_C4119558_C_158d237e9d19c8312d039d927a8ffa7e48dfc5d7c2bf5503110a88a86ba01a"
COMPANY_ID = "biz_uZIgn00JqEYqUL"
PLAN_ID    = "plan_7maR6zKtPQlyL"

client = Whop(api_key=API_KEY)

# =========================
# 1. GET ALL MEMBERS
# =========================
members = []

page = client.members.list(company_id=COMPANY_ID)

while True:
    for member in page.data:
        members.append(member.id)

    if not page.page_info.has_next_page:
        break

    page = client.members.list(
        company_id=COMPANY_ID,
        cursor=page.page_info.end_cursor
    )

print(f"👥 Members trouvés : {len(members)}")

# =========================
# 2. CREATE PAYMENTS
# =========================
for member_id in members:
    pm_page = client.payment_methods.list(member_id=member_id)

    while True:
        for pm in pm_page.data:
            try:
                payment = client.payments.create(
                    company_id=COMPANY_ID,
                    member_id=member_id,
                    payment_method_id=pm.id,
                    plan_id=PLAN_ID
                )

                print(f"✅ SUCCESS | {member_id} | {pm.id} | Payment ID: {payment.id}")

            except Exception as e:
                print(f"❌ FAILED  | {member_id} | {pm.id} | Reason: {e}")

        if not pm_page.page_info.has_next_page:
            break

        pm_page = client.payment_methods.list(
            member_id=member_id,
            cursor=pm_page.page_info.end_cursor
        )