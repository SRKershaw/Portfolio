// src/components/Dashboard.jsx - Main dashboard with resizable panels

import { useState, useEffect } from 'react';
import RGL, { WidthProvider } from 'react-grid-layout';
import PortfolioSelector from './PortfolioSelector';
import AssetTable from './AssetTable';
import AllocationChart from './AllocationChart';
import SetDropZone from './SetDropZone';
import { useApi } from '../hooks/useApi';

const ReactGridLayout = WidthProvider(RGL);

function Dashboard() {
  const { sendRequest } = useApi();
  const [selectedPortfolio, setSelectedPortfolio] = useState(null);
  const [assets, setAssets] = useState([]);

  useEffect(() => {
    if (selectedPortfolio) {
      const fetchPortfolio = async () => {
        const data = await sendRequest('GET', `/portfolios/${selectedPortfolio}`);
        // Flatten assets from sets for table (extend to per-set later)
        const allAssets = data.sets.flatMap(s => s.assets);
        setAssets(allAssets);
      };
      fetchPortfolio();
    }
  }, [selectedPortfolio, sendRequest]);

  const layout = [
    { i: 'selector', x: 0, y: 0, w: 12, h: 2, static: true },
    { i: 'table', x: 0, y: 2, w: 6, h: 8 },
    { i: 'chart', x: 6, y: 2, w: 6, h: 8 }
  ];

  const onDragEnd = (result) => {
    // Handle asset move between sets (backend PATCH later)
    if (!result.destination) return;
    console.log('Asset moved from index', result.source.index, 'to', result.destination.index);
  };

  return (
    <ReactGridLayout className="layout" layout={layout} cols={12} rowHeight={30} width={1200}>
      <div key="selector">
        <PortfolioSelector onSelect={setSelectedPortfolio} />
      </div>
      <div key="table">
        <SetDropZone setId="main">
          <AssetTable assets={assets} onEdit={/* backend PUT */} onDragEnd={onDragEnd} />
        </SetDropZone>
      </div>
      <div key="chart">
        <AllocationChart assets={assets} />
      </div>
    </ReactGridLayout>
  );
}

export default Dashboard;