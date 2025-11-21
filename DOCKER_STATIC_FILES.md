# Docker Static Files Configuration

## Problem
When running Django in Docker with production settings (`DEBUG=False`), static files (including Django admin CSS/JS) are not automatically served by Django. This causes the admin panel and other pages to appear without styling.

## Solution
This project uses **WhiteNoise** to serve static files efficiently in production without requiring a separate web server like Nginx.

### Changes Made

1. **Added WhiteNoise to requirements.txt**
   - `whitenoise>=6.6.0`

2. **Fixed BASE_DIR path in settings/base.py**
   - Changed from `parent.parent` to `parent.parent.parent` to correctly point to project root
   - This ensures STATIC_ROOT and MEDIA_ROOT point to the correct directories

3. **Added WhiteNoise middleware**
   - Placed after `SecurityMiddleware` and before other middleware
   - Enables serving of static files in production

4. **Configured static files storage**
   - Using `CompressedManifestStaticFilesStorage` for optimal performance
   - Automatically compresses and caches static files

## Usage

### Running with Docker Compose

```bash
# Build and start containers
docker-compose up --build

# The admin panel should now have proper styling at:
# http://127.0.0.1:8000/admin/
```

### Running Locally (Development)

```bash
# With development settings (DEBUG=True)
python manage.py runserver

# Static files are served automatically
```

### Collecting Static Files

Static files are automatically collected when the Docker container starts (via the command in docker-compose.yml).

To manually collect static files:

```bash
# Inside container
python manage.py collectstatic --noinput

# Or locally with production settings
python manage.py collectstatic --noinput --settings=project.settings.production
```

## How It Works

1. **WhiteNoise Middleware**: Intercepts requests for static files and serves them directly from the `staticfiles/` directory
2. **collectstatic**: Gathers all static files from installed apps (including Django admin) into `STATIC_ROOT`
3. **CompressedManifestStaticFilesStorage**: 
   - Creates compressed versions of static files (.gz)
   - Generates unique filenames with content hashes for cache busting
   - Creates a manifest file to map original names to hashed names

## File Locations

- **Static files source**: Various app directories (e.g., `dogs/static/`, Django admin static files)
- **Collected static files**: `/home/engine/project/staticfiles/` (in Docker: `/app/staticfiles/`)
- **Media files**: `/home/engine/project/media/` (in Docker: `/app/media/`)

## Troubleshooting

### Admin CSS still not loading?

1. **Rebuild the Docker image**:
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up
   ```

2. **Check if collectstatic ran successfully**:
   ```bash
   docker-compose logs web | grep collectstatic
   ```
   Should show: "129 static files copied to '/app/staticfiles'"

3. **Verify WhiteNoise is installed**:
   ```bash
   docker-compose exec web pip show whitenoise
   ```

4. **Check staticfiles directory exists**:
   ```bash
   docker-compose exec web ls -la /app/staticfiles/admin/
   ```

### Browser cache issues

If you previously loaded the page without styles, clear your browser cache or do a hard refresh:
- Chrome/Firefox: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Or open in incognito/private window

## Additional Notes

- WhiteNoise works with any WSGI server (Gunicorn, uWSGI, etc.)
- No need for Nginx or Apache to serve static files (though you can still use them if needed)
- Static files are served with proper caching headers for performance
- Compressed versions are automatically served to clients that support gzip encoding
