// frontend/src/components/Dashboard.jsx - Fixed layout with data-grid
// ########################################################################################

import { useState, useEffect } from 'react';
import RGL, { WidthProvider } from 'react-grid-layout';
import { DragDropContext } from '@hello-pangea/dnd';
import PortfolioSelector from './PortfolioSelector';
import AssetTable from './AssetTable';
import AllocationChart from './AllocationChart';
import SetDropZone from './SetDropZone';
import { useApi } from '../hooks/useApi';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

const ReactGridLayout = WidthProvider(RGL);

function Dashboard() {
  const { sendRequest, loading: apiLoading, error: apiError } = useApi();
  const [selectedPortfolio, setSelectedPortfolio] = useState(null);
  const [assets, setAssets] = useState([]);
  const [debug, setDebug] = useState('');

  useEffect(() => {
    if (selectedPortfolio) {
      const fetchPortfolio = async () => {
        try {
          const data = await sendRequest('GET', `/portfolios/${selectedPortfolio}`);
          setDebug(`Fetched: ${data.name}, ${data.sets.length} sets, ${data.sets.flatMap(s => s.assets).length} assets`);
          const allAssets = data.sets.flatMap(s => s.assets.map(a => ({ ...a, id: a.id })));
          setAssets(allAssets);
        } catch (err) {
          setDebug(`Error: ${err.message}`);
        }
      };
      fetchPortfolio();
    }
  }, [selectedPortfolio, sendRequest]);

  const handleDragEnd = (result) => {
    if (!result.destination) return;
    console.log('Drag result:', result);
  };

  const handleEdit = (row) => {
    console.log('Edit row:', row);
  };

  if (apiError) return <div style={{ padding: '2rem', color: 'red' }}>API Error: {apiError}</div>;
  if (apiLoading) return <div style={{ padding: '2rem' }}>Loading...</div>;

  return (
    <div style={{ padding: '1rem', background: '#1a1a1a', color: '#fff', minHeight: '100vh' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '1rem' }}>Portfolio App</h1>
      <h2 style={{ textAlign: 'center', marginBottom: '1rem' }}>Portfolio Dashboard</h2>

      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <PortfolioSelector onSelect={setSelectedPortfolio} />
        {debug && (
          <p style={{ fontFamily: 'monospace', background: '#333', padding: '8px', margin: '8px 0', borderRadius: '4px' }}>
            {debug}
          </p>
        )}

        {!selectedPortfolio ? (
          <p style={{ textAlign: 'center', marginTop: '2rem' }}>Select a portfolio to begin.</p>
        ) : assets.length === 0 ? (
          <p style={{ textAlign: 'center', marginTop: '2rem' }}>No assets found.</p>
        ) : (
          <DragDropContext onDragEnd={handleDragEnd}>
            <ReactGridLayout
              className="layout"
              cols={12}
              rowHeight={60}
              width={1200}
              margin={[20, 20]}
              containerPadding={[0, 0]}
            >
              <div key="table" data-grid={{ x: 0, y: 0, w: 7, h: 9 }}>
                <div style={{ background: '#2d2d2d', padding: '1rem', borderRadius: '8px', height: '100%' }}>
                  <h3 style={{ margin: '0 0 1rem 0' }}>Assets</h3>
                  <SetDropZone setId="main">
                    <div style={{ height: 'calc(100% - 40px)', overflow: 'auto' }}>
                      <AssetTable assets={assets} onEdit={handleEdit} />
                    </div>
                  </SetDropZone>
                </div>
              </div>

              <div key="chart" data-grid={{ x: 7, y: 0, w: 5, h: 9 }}>
                <div style={{ background: '#2d2d2d', padding: '1rem', borderRadius: '8px', height: '100%' }}>
                  <h3 style={{ margin: '0 0 1rem 0' }}>Allocation</h3>
                  <div style={{ height: 'calc(100% - 40px)' }}>
                    <AllocationChart assets={assets} />
                  </div>
                </div>
              </div>
            </ReactGridLayout>
          </DragDropContext>
        )}
      </div>
    </div>
  );
}

export default Dashboard;