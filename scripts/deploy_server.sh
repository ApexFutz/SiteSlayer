#!/bin/bash
# Script to deploy the SiteSlayer web server to Fly.io.

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Function to check if Fly CLI is installed
check_fly_cli() {
    if command -v fly &> /dev/null; then
        FLY_VERSION=$(fly version 2>/dev/null | head -n 1)
        echo "✓ Fly CLI found: $FLY_VERSION"
        return 0
    else
        echo "✗ Fly CLI not found. Please install it first:"
        echo "  https://fly.io/docs/getting-started/installing-flyctl/"
        return 1
    fi
}

# Function to check if user is authenticated with Fly.io
check_fly_auth() {
    if fly auth whoami &> /dev/null; then
        return 0
    else
        echo "✗ Not authenticated with Fly.io. Please run:"
        echo "  fly auth login"
        return 1
    fi
}

# Main deployment function
deploy() {
    echo "🚀 Deploying SiteSlayer to Fly.io..."
    echo "📁 Project root: $PROJECT_ROOT"
    echo ""
    
    # Check prerequisites
    if ! check_fly_cli; then
        exit 1
    fi
    
    if ! check_fly_auth; then
        exit 1
    fi
    
    # Change to project root directory
    cd "$PROJECT_ROOT" || exit 1
    
    # Run fly deploy
    echo "📦 Starting deployment..."
    
    # Handle Ctrl+C gracefully
    trap 'echo ""; echo "⚠️  Deployment cancelled by user."; exit 1' INT
    
    if fly deploy; then
        echo ""
        echo "✅ Deployment successful!"
        echo ""
        echo "Your application should be available at:"
        echo "  https://slaydigital.fly.dev"
    else
        echo ""
        echo "❌ Deployment failed. Check the output above for details."
        exit 1
    fi
}

# Run deployment
deploy

