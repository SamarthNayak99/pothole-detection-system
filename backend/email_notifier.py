import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_pothole_notification(pothole_id, latitude, longitude, confidence, timestamp, image_path):
    """
    Sends an email notification for a detected pothole.
    """
    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = os.getenv("EMAIL_RECEIVER")

    if not sender_email or not sender_password or not receiver_email:
        print("❌ Error: Missing email credentials in environment variables.")
        return False

    try:
        # Create Email Message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"🚨 POTHOLE ALERT: Detected with {confidence*100:.1f}% Confidence"

        # Formatted Date
        try:
            dt_obj = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            formatted_time = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        except:
            formatted_time = timestamp

        # Google Maps Link
        maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

        # Email Body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
                <h2 style="color: #d9534f; margin-top: 0;">🚨 Pothole Detected!</h2>
                
                <p><strong>Pothole ID:</strong> #{pothole_id}</p>
                <p><strong>Detection Time:</strong> {formatted_time}</p>
                <p><strong>Confidence Score:</strong> <strong>{confidence*100:.1f}%</strong></p>
                
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                
                <h3 style="color: #4285f4; margin-bottom: 5px;">📍 Location Details</h3>
                <p style="margin: 0;"><strong>Latitude:</strong> {latitude}</p>
                <p style="margin: 0;"><strong>Longitude:</strong> {longitude}</p>
                
                <div style="margin: 20px 0;">
                    <a href="{maps_link}" style="background-color: #4285f4; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                        🗺️ View on Google Maps
                    </a>
                </div>

                <p style="font-size: 0.9em; color: #777;">
                    Please check the attached image for visual verification.
                </p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))

        # Attach Image (if exists)
        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data, name=os.path.basename(image_path))
                    msg.attach(image)
                print(f"📎 Image attached: {os.path.basename(image_path)}")
            except Exception as img_err:
                print(f"⚠️ Could not attach image: {img_err}")
        else:
            print(f"⚠️ Image file not found at: {image_path}")

        # Send via SMTP
        print(f"📧 Sending email to {receiver_email}...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print("✅ Email Alert Sent Successfully!")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
