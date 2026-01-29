"""Quick test dengan 1 URL saja"""
from website_comparator import WebsiteComparator

print("Testing dengan 1 URL dari setiap website...")
print("=" * 70)

comparator = WebsiteComparator()

result = comparator.compare(
    website_a_urls=["https://iot-fakeapi.vercel.app/petengoran/station1"],
    website_b_urls=["https://danigrafana.grafana.net/public-dashboards/f007adeb80044a9c9e2dac43ac0ea77a"],
    website_a_name="IoT Dashboard",
    website_b_name="Grafana Dashboard"
)

print("\n" + "=" * 70)
print("✓ Test selesai!")
print(f"✓ PDF: {result['pdf_path']}")
print("=" * 70)
