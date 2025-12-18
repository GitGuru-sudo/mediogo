# Deployment Guide for MediGo on Render

## Prerequisites
1. A Render account (https://render.com)
2. Your code pushed to a GitHub repository (public or private)

## Step-by-Step Deployment Instructions

### 1. **Push Your Code to GitHub**
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. **Connect Your Repository to Render**
1. Go to https://render.com and sign in
2. Click "New +" and select "Web Service"
3. Click "Connect a repository"
4. Search for your medigo repository and connect it
5. Click "Connect"

### 3. **Configure Your Web Service**
On the Render dashboard, fill in:

- **Name**: medigo (or your preferred name)
- **Environment**: Python 3
- **Build Command**: `bash ./build.sh`
- **Start Command**: `gunicorn medigo.wsgi:application`
- **Instance Type**: Free (or paid if needed)
- **Region**: Select your preferred region (Ohio is default)

### 4. **Add Environment Variables**
In the Render dashboard, go to "Environment" and add:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11` |
| `DEBUG` | `false` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
| `SECRET_KEY` | Generate a new secure key (see below) |

**To generate a secure SECRET_KEY:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 5. **Deploy**
1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Monitor the deployment in the "Logs" tab
4. Once deployment is complete, your app will be live at `https://your-app-name.onrender.com`

## Important Notes

### Database Migration
The `build.sh` script automatically runs migrations. Your first deployment will:
- Install dependencies from `requirements.txt`
- Collect static files
- Run migrations

### Static Files
- WhiteNoise is configured to serve static files
- CSS, JavaScript, and images will be served automatically

### Current Limitations (Free Plan)
- Services spin down after 15 minutes of inactivity
- 0.5GB RAM
- Limited compute

### Database Considerations
Currently, your project uses SQLite (db.sqlite3). For production, consider:
- **Option 1**: Keep SQLite (simple, free, but limited)
- **Option 2**: Add PostgreSQL from Render
  - Add PostgreSQL database from Render dashboard
  - Update `DATABASE_URL` environment variable
  - Update `settings.py` to use PostgreSQL

### Debugging Issues
Check the Logs tab in Render dashboard for:
- Build errors
- Migration errors
- Runtime errors

### Updating Your App
After making changes:
```bash
git add .
git commit -m "Your changes"
git push origin main
```
Render will automatically redeploy your application.

## Additional Resources
- Render Documentation: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
