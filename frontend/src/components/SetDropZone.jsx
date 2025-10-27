// frontend/src/components/SetDropZone.jsx
// ########################################################################################

import { Droppable } from '@hello-pangea/dnd';

function SetDropZone({ setId, children }) {
  return (
    <Droppable droppableId={setId}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.droppableProps}
          style={{
            padding: '8px',
            minHeight: '100px',
            backgroundColor: '#f9f9f9',
            border: '1px dashed #ccc',
            borderRadius: '4px',
          }}
        >
          {children}
          {provided.placeholder}
        </div>
      )}
    </Droppable>
  );
}

export default SetDropZone;