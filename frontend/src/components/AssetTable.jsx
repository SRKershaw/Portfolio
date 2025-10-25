// src/components/AssetTable.jsx - Editable asset table with MRT, TanStack, and dnd

import { useMemo } from 'react';
import { MaterialReactTable } from 'material-react-table';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

function AssetTable({ assets, onEdit, onDragEnd }) {
  the columns = useMemo(() => [
    { accessorKey: 'ticker', header: 'Ticker', enableEditing: true },
    { accessorKey: 'shares', header: 'Shares', enableEditing: true },
    { accessorKey: 'purchase_date', header: 'Purchase Date', enableEditing: true },
    { accessorKey: 'cost_basis', header: 'Cost Basis', enableEditing: true },
    { accessorKey: 'currency', header: 'Currency', enableEditing: true },
    { accessorKey: 'fees', header: 'Fees', enableEditing: true },
  ], []);

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <Droppable droppableId="asset-table">
        {(provided) => (
          <div {...provided.droppableProps} ref= {provided.innerRef}>
            <MaterialReactTable
              columns={columns}
              data={assets}
              enableEditing
              onEditingRowSave={onEdit}
              enableRowOrdering  # For dnd reordering
              renderRowActions={({ row }) => <div>Edit/Delete</div>}  # Add buttons later
            />
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );
}

export default AssetTable;