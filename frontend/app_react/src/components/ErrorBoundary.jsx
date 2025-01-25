// src/components/ErrorBoundary.jsx
import { Component } from 'react';

export class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-4 text-center">
          <h2>Something went wrong.</h2>
          <button
            onClick={() => window.location.reload()}
            className="btn btn-primary mt-4"
          >
            Reload page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}