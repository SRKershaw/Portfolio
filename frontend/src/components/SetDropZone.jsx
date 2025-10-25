// src/components/SetDropZone.jsx - Dnd target for sets (move assets)

import { Droppable } from 'react-beautiful-dnd';

function SetDropZone({ setId, children }) {
  return (
    <Droppable droppableId={setId}>
      {(provided) => (
        <div ref={provided.innerRef} {...provided.droppableProps}>
          {children}
          {provided.placeholder}
        </div>
      )}
    </Droppable>
  );
}

export default SetDropZone;