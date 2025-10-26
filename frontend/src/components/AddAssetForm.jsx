// src/components/AddAssetForm.jsx - MUI form for adding asset

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button, TextField, Box } from '@mui/material';

const schema = z.object({
  ticker: z.string().min(1, 'Ticker required').max(10),
  shares: z.number().min(1, 'Shares > 0'),
  purchase_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Date YYYY-MM-DD'),
  cost_basis: z.number().min(0, 'Cost >= 0'),
  currency: z.string().length(3, 'Currency 3 letters'),
  fees: z.number().min(0, 'Fees >= 0').optional(),
});

function AddAssetForm({ onSubmit, onCancel }) {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema)
  });

  const submit = (data) => {
    onSubmit(data);
  };

  return (
    <Box component="form" onSubmit={handleSubmit(submit)} sx={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <TextField label="Ticker" {...register('ticker')} error={!!errors.ticker} helperText={errors.ticker?.message} />
      <TextField label="Shares" type="number" {...register('shares', { valueAsNumber: true })} error={!!errors.shares} helperText={errors.shares?.message} />
      <TextField label="Purchase Date (YYYY-MM-DD)" {...register('purchase_date')} error={!!errors.purchase_date} helperText={errors.purchase_date?.message} />
      <TextField label="Cost Basis" type="number" {...register('cost_basis', { valueAsNumber: true })} error={!!errors.cost_basis} helperText={errors.cost_basis?.message} />
      <TextField label="Currency" {...register('currency')} error={!!errors.currency} helperText={errors.currency?.message} />
      <TextField label="Fees" type="number" {...register('fees', { valueAsNumber: true })} error={!!errors.fees} helperText={errors.fees?.message} />
      <Button variant="contained" type="submit">Add</Button>
      <Button variant="outlined" onClick={onCancel}>Cancel</Button>
    </Box>
  );
}

export default AddAssetForm;