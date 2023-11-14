from firebase_admin import auth, firestore
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

def verify_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return True, uid
    except auth.ExpiredIdTokenError:
        return None, "Token expired"
    except auth.InvalidIdTokenError:
        return None, "Invalid token"
    except Exception as e:
        # Handle other exceptions if needed
        return None, f"Token verification failed: {e}"

    
def is_username_unique(username):
    firestore_db = firestore.client()

    try:
        # Query the Firestore collection to check if any user has the given username
        user_query = firestore_db.collection("users").where("username", "==", username).limit(1)
        existing_user = user_query.stream()

        # If existing_user is empty, the username is unique
        return not any(existing_user)
    except Exception as e:
        # Handle Firestore query errors
        print(f"Error querying Firestore: {e}")
        return False
    
def send_email(link, recipient, user): 
    with get_connection(  
        host=settings.EMAIL_HOST, 
    port=settings.EMAIL_PORT,  
    username=settings.EMAIL_HOST_USER, 
    password=settings.EMAIL_HOST_PASSWORD, 
    use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = 'Verify your email for CarLendar App'
        email_from = settings.EMAIL_HOST_USER  
        recipient_list = [recipient]  
        message = f'''<p>Hello {user},</p>
        <p>Follow this link to verify your email address.</p>
        <p><a href='{link}'>{link}</a></p>
        <p>If you didn’t ask to verify this address, you can ignore this email.</p>
        <p>Thanks,</p>
        <p>Your CarLendar team</p>''' 
        msg = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
        msg.content_subtype = "html"
        msg.send() 