import { useEffect, useState } from 'react';
import { useSearchParams } from '@remix-run/react';
import { useConfig, getCsrfToken } from "../components/ConfigProvider";

export default function AuthCallback() {
  const [searchParams] = useSearchParams();
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { configServerUrl } = useConfig();

  useEffect(() => {
    const exchangeCode = async () => {
      const tempCode = searchParams.get('temp_code');
      
      if (!tempCode) {
        setError('No temporary code provided');
        return;
      }
      try {
        const csrfToken = await getCsrfToken()
        const response = await fetch(`${configServerUrl}/exchange-temp-code`, {
          method: 'POST',
          credentials: "include",
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrfToken ?? '',
          },
          body: JSON.stringify({ temp_code: tempCode }),
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || 'Failed to exchange code');
        }
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        setToken(data.access_token);
      } catch (err: any) {
        setError(err.message);
      }
    };
    exchangeCode();
  }, [searchParams]);

  const renderContent = () => {
    if (error) {
      return (
        <div className="text-red-500">
          <h2>Error</h2>
          <p>{error}</p>
        </div>
      );
    }

    if (token) {
      return (
        <div className="space-y-4">
          <h2 className="text-2xl">Successfully Authenticated!</h2>
          <button 
            onClick={() => window.location.href = '/'}
            className="bg-solace-green text-white px-6 py-2 rounded shadow hover:bg-solace-dark-green"
          >
            Go to Chat
          </button>
        </div>
      );
    }

    return <div>Processing authentication...</div>;
  };

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 flex items-center justify-center">
      <div className="text-center p-8 max-w-lg">
        {renderContent()}
      </div>
    </div>
  );
}