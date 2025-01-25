import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import Layout from './components/layout/Layout';
import { AlarmGrid } from './components/alarms/AlarmGrid';
import { AlarmStats } from './components/alarms/AlarmStats';
import { AlarmFilters } from 'components/alarms/AlarmFilters';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Layout>
        <div className="space-y-6">
          <AlarmStats />
          <AlarmFilters />
          <AlarmGrid />
        </div>
      </Layout>
      <Toaster position="top-right" />
    </QueryClientProvider>
  );
}

export default App;
