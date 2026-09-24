from services.db import init_db, create_user
from services.validation import validate_phone

init_db()

demo_users = [
    ("Demo User 1", "+919876543210", 17.3850, 78.4867, "Hyderabad", True,
     ["Moderate Risk", "High Risk", "Very High Risk", "Critical Risk"]),
    ("Demo User 2", "+919876543211", 17.4000, 78.4800, "Nearby Hyderabad", True,
     ["Low Risk", "Moderate Risk", "High Risk", "Very High Risk", "Critical Risk"]),
    ("Demo User 3", "+919876543212", 17.7000, 78.9000, "Outside demo radius", True,
     ["High Risk", "Very High Risk", "Critical Risk"]),
]

for row in demo_users:
    ok, _ = validate_phone(row[1])
    if ok:
        try:
            create_user(*row)
        except Exception:
            pass

print("Demo users inserted. Run: streamlit run app.py")
