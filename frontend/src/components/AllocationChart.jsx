// src/components/AllocationChart.jsx - Highcharts pie for portfolio allocation

import { useEffect, useRef } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

function AllocationChart({ assets }) {
  const chartRef = useRef(null);

  useEffect(() => {
    Highcharts.chart(chartRef.current.container, {
      chart: { type: 'pie' },
      title: { text: 'Portfolio Allocation' },
      series: [{
        name: 'Allocation',
        data: assets.map(a => ({
          name: a.ticker,
          y: a.shares * a.cost_basis,  # Simple allocation (extend to current value later)
        }))
      }]
    });
  }, [assets]);

  return <HighchartsReact ref={chartRef} highcharts={Highcharts} />;
}

export default AllocationChart;