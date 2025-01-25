# Initial setup
./setup.sh

# Development
uv run dev-backend  # Start FastAPI server
uv run dev-frontend # Start Vite dev server

# Package management
uv pip install package-name  # Install Python package
uv npm install package-name  # Install Node.js package

# Quality checks
uv run format  # Run Black formatter
uv run lint    # Run MyPy type checker
uv run test    # Run pytest

# Build for production
uv run build   # Build frontend