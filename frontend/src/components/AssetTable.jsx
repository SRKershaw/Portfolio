// frontend/src/components/AssetTable.jsx - Wide, editable table with small text
// ########################################################################################

// PURPOSE: Display assets, allow inline edit, wide by default
// EDITING: Change column sizes, font size, or minWidth

import { useMemo } from 'react';
import { MaterialReactTable } from 'material-react-table';

function AssetTable({ assets, onEdit }) {
  // COLUMNS: Define width and editing
  const columns = useMemo(() => [
    { accessorKey: 'ticker', header: 'Ticker', size: 100, enableEditing: true },
    { accessorKey: 'shares', header: 'Shares', size: 90, enableEditing: true },
    { accessorKey: 'purchase_date', header: 'Purchase Date', size: 140, enableEditing: true },
    { accessorKey: 'cost_basis', header: 'Cost Basis', size: 120, enableEditing: true },
    { accessorKey: 'currency', header: 'Currency', size: 90, enableEditing: true },
    { accessorKey: 'fees', header: 'Fees', size: 90, enableEditing: true },
  ], []);

  return (
    // TABLE: minWidth ensures wide default, scroll if smaller screen
    <MaterialReactTable
      columns={columns}
      data={assets}
      enableEditing
      onEditingRowSave={onEdit}
      enableColumnOrdering
      enableGlobalFilter

      // CONTAINER: Wide by default, scroll only when needed
      muiTableContainerProps={{
        sx: { 
          minWidth: 1200,           // ← Makes table wide by default
          overflowX: 'auto',        // ← Scroll only if screen < 1200px
          '& .MuiTable-root': { 
            tableLayout: 'fixed'    // ← Ensures column widths respected
          }
        }
      }}

      // CELL TEXT: Smaller font
      muiTableBodyCellProps={{
        sx: { 
          fontSize: '0.875rem',     // ← Smaller text
          padding: '8px'            // ← Tighter padding
        }
      }}

      // HEADER: Slightly smaller
      muiTableHeadCellProps={{
        sx: { 
          fontSize: '0.875rem',
          fontWeight: 600
        }
      }}
    />
  );
}

export default AssetTable;