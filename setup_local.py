import os
import sys
import subprocess
import shutil

def setup_local_environment():
    print("🚀 Setting up Medigo local development environment...\n")
    
    # Create .env file if it doesn't exist
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    env_example = os.path.join(os.path.dirname(__file__), '.env.example')
    
    if not os.path.exists(env_file) and os.path.exists(env_example):
        print("🔧 Creating .env file from example...")
        shutil.copy(env_example, env_file)
        print("✅ Created .env file")
    
    # Install Python dependencies
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return
    
    # Run migrations
    print("\n🔄 Running database migrations...")
    try:
        subprocess.check_call([sys.executable, "manage.py", "migrate"])
        print("✅ Database migrations completed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running migrations: {e}")
        return
    
    # Create superuser (optional)
    create_superuser = input("\n👤 Do you want to create a superuser? (y/n): ").strip().lower()
    if create_superuser == 'y':
        try:
            subprocess.check_call([sys.executable, "manage.py", "createsuperuser"], shell=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error creating superuser: {e}")
    
    print("\n✨ Setup complete! You can now start the development server with:")
    print("  python manage.py runserver\n")

if __name__ == "__main__":
    setup_local_environment()
