// frontend/src/components/PortfolioSelector.jsx - Dropdown to fetch and select portfolios from backend
// ########################################################################################

import { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';

function PortfolioSelector({ onSelect }) {
  const { sendRequest, loading, error } = useApi();
  const [portfolios, setPortfolios] = useState([]);
  const [selected, setSelected] = useState('');

  useEffect(() => {
    const fetchPortfolios = async () => {
      const data = await sendRequest('GET', '/portfolios');
      setPortfolios(data);
      if (data.length > 0) {
        setSelected(data[0].id);
        onSelect(data[0].id);  // Auto-select first
      }
    };
    fetchPortfolios();
  }, [sendRequest, onSelect]);

  const handleChange = (e) => {
    setSelected(e.target.value);
    onSelect(e.target.value);
  };

  if (error) return <p>Error: {error}</p>;
  if (loading) return <p>Loading portfolios...</p>;

  return (
    <FormControl fullWidth>
      <InputLabel>Portfolio</InputLabel>
      <Select value={selected} onChange= {handleChange}>
        {portfolios.map(p => (
          <MenuItem key={p.id} value={p.id}>
            {p.name}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}

export default PortfolioSelector;