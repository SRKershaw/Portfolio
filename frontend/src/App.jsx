// frontend/src/App.jsx - Main app with clean layout, wide table, and full comments
// ########################################################################################

// PURPOSE: Display portfolio selector, Add button, and wide asset table
// EDITING: Change maxWidth, colors, or spacing in sx props

import { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Button, 
  Modal, 
  Box, 
  Select, 
  MenuItem, 
  FormControl, 
  InputLabel 
} from '@mui/material';
import PortfolioSelector from './components/PortfolioSelector'; // Dropdown for portfolios
import AssetTable from './components/AssetTable'; // Editable table with wide layout
import AddAssetForm from './components/AddAssetForm'; // Modal form for new assets
import { useApi } from './hooks/useApi'; // Reusable API hook
import './App.css';

function App() {
  // STATE: Portfolio list, selected ID, data, modal open
  const { sendRequest } = useApi();
  const [selectedPortfolio, setSelectedPortfolio] = useState('');
  const [portfolioData, setPortfolioData] = useState(null);
  const [openAddModal, setOpenAddModal] = useState(false);
  const [portfolios, setPortfolios] = useState([]);

  // EFFECT: Fetch all portfolios on mount
  useEffect(() => {
    const fetchPortfolios = async () => {
      const data = await sendRequest('GET', '/portfolios');
      setPortfolios(data);
      if (data.length > 0) setSelectedPortfolio(data[0].id); // Auto-select first
    };
    fetchPortfolios();
  }, [sendRequest]);

  // EFFECT: Fetch selected portfolio data when ID changes
  useEffect(() => {
    if (selectedPortfolio) {
      const fetchPortfolio = async () => {
        const data = await sendRequest('GET', `/portfolios/${selectedPortfolio}`);
        setPortfolioData(data);
      };
      fetchPortfolio();
    }
  }, [selectedPortfolio, sendRequest]);

  // MODAL: Close add form
  const handleAddClose = () => setOpenAddModal(false);

  // ADD ASSET: POST to first set, then refresh
  const handleAddSubmit = async (formData) => {
    if (!portfolioData?.sets?.[0]?.id) return;
    const setId = portfolioData.sets[0].id;
    await sendRequest('POST', `/sets/${setId}/assets`, formData);
    const updated = await sendRequest('GET', `/portfolios/${selectedPortfolio}`);
    setPortfolioData(updated);
    setOpenAddModal(false);
  };

  // EDIT ASSET: PUT update, then refresh
  const handleEdit = async (updatedAsset) => {
    await sendRequest('PUT', `/assets/${updatedAsset.id}`, updatedAsset);
    const updated = await sendRequest('GET', `/portfolios/${selectedPortfolio}`);
    setPortfolioData(updated);
  };

  return (
    // CONTAINER: Full width, padding, dark background
    <Container maxWidth={false} sx={{ py: 4, px: { xs: 2, md: 4 }, bgcolor: '#121212', minHeight: '100vh' }}>
      
      {/* TITLE: Centered, bold, white */}
      <Typography 
        variant="h3" 
        align="center" 
        gutterBottom 
        sx={{ fontWeight: 600, color: '#fff', mb: 4 }}
      >
        Portfolio App
      </Typography>

      {/* DROPDOWN: Centered, dark background, light text */}
      <Box sx={{ maxWidth: 500, mx: 'auto', mb: 4 }}>
        <FormControl fullWidth>
          <InputLabel sx={{ color: '#aaa' }}>Select Portfolio</InputLabel>
          <Select
            value={selectedPortfolio}
            onChange={(e) => setSelectedPortfolio(e.target.value)}
            label="Select Portfolio"
            sx={{
              bgcolor: '#2d2d2d',
              color: '#fff',
              '& .MuiSelect-icon': { color: '#fff' },
              '& .MuiOutlinedInput-notchedOutline': { borderColor: '#555' },
              '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: '#777' },
            }}
          >
            {portfolios.map(p => (
              <MenuItem key={p.id} value={p.id} sx={{ color: '#fff' }}>
                {p.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {/* CONTENT: Only show when portfolio selected */}
      {selectedPortfolio && portfolioData ? (
        <Box>
          {/* ADD BUTTON: Centered, large */}
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
            <Button 
              variant="contained" 
              size="large"
              onClick={() => setOpenAddModal(true)}
              sx={{ px: 5, py: 1.5, fontSize: '1.1rem' }}
            >
              Add Asset
            </Button>
          </Box>

          {/* TABLE: Full width, scroll only if needed */}
          <Box sx={{ width: '100%', overflowX: 'auto' }}>
            <AssetTable 
              assets={portfolioData.sets.flatMap(s => s.assets)} 
              onEdit={handleEdit}
            />
          </Box>
        </Box>
      ) : (
        // EMPTY STATE: Centered message
        <Typography variant="h6" align="center" sx={{ mt: 6, color: '#aaa' }}>
          Select a portfolio to view assets.
        </Typography>
      )}

      {/* MODAL: Add asset form */}
      <Modal open={openAddModal} onClose={handleAddClose}>
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          bgcolor: 'background.paper',
          p: 4,
          borderRadius: 2,
          width: { xs: '90%', sm: 500 },
          maxHeight: '90vh',
          overflow: 'auto'
        }}>
          <AddAssetForm onSubmit={handleAddSubmit} onCancel={handleAddClose} />
        </Box>
      </Modal>
    </Container>
  );
}

export default App;