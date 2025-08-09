import os
import sys

print("🚀 LAUNCHING INVESTMENT ADVISOR PROTOTYPE")
print("=" * 50)
print()
print("📊 Starting Streamlit dashboard...")
print("🌐 App will be available at: http://localhost:8501")
print("📱 For mobile: http://your-ip:8501")
print()
print("⏳ Launching in 3 seconds...")

# Simple countdown
import time
for i in range(3, 0, -1):
    print(f"   {i}...")
    time.sleep(1)

print()
print("🎯 Starting app now!")

# Launch Streamlit directly
os.system("streamlit run src/app/streamlit_app.py")