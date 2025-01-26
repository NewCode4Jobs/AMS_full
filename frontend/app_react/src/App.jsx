import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import Layout from './components/layout/Layout';
import { AlarmGrid } from './components/alarms/AlarmGrid';
import { AlarmStats } from './components/alarms/AlarmStats';
import { AlarmFilters } from './components/alarms/AlarmFilters';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: true,
      refetchOnMount: true,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-vh-100 d-flex flex-column">
        <Layout>
          <div className="flex-grow-1">
            <div className="row h-100 g-4">
              {/* Left Column - Filters */}
              <div className="col-md-3">
                <div className="card shadow-sm h-100">
                  <div className="card-body">
                    <AlarmFilters />
                  </div>
                </div>
              </div>

              {/* Middle Column - Main Content */}
              <div className="col-md-6">
                <div className="card shadow-sm h-100">
                  <div className="card-body">
                    <AlarmGrid />
                  </div>
                </div>
              </div>

              {/* Right Column - Stats */}
              <div className="col-md-3">
                <div className="card shadow-sm h-100">
                  <div className="card-body">
                    <AlarmStats />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Layout>
        <Toaster position="top-right" />
      </div>
    </QueryClientProvider>
  );
}

export default App;
