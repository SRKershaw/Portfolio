// src/components/AllocationChart.jsx - Highcharts pie with NaN guard

import { useEffect, useRef } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import 'highcharts/modules/accessibility'; // Optional: silence warning

function AllocationChart({ assets }) {
  const chartRef = useRef(null);

  const chartData = assets
    .map(a => {
      const value = a.shares * a.cost_basis;
      return isNaN(value) || !isFinite(value) ? null : {
        name: a.ticker,
        y: value
      };
    })
    .filter(Boolean);

  const hasData = chartData.length > 0;

  const options = {
    chart: { type: 'pie', height: '100%' },
    title: { text: hasData ? 'Portfolio Allocation' : 'No Data' },
    tooltip: { pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>' },
    accessibility: { enabled: true },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        dataLabels: {
          enabled: true,
          format: '<b>{point.name}</b>: {point.percentage:.1f} %'
        }
      }
    },
    series: [{
      name: 'Allocation',
      colorByPoint: true,
      data: hasData ? chartData : [{ name: 'No Assets', y: 1, color: '#ccc' }]
    }]
  };

  return (
    <div style={{ width: '100%', height: '100%', minHeight: '300px' }}>
      <HighchartsReact
        highcharts={Highcharts}
        options={options}
        ref={chartRef}
      />
    </div>
  );
}

export default AllocationChart;