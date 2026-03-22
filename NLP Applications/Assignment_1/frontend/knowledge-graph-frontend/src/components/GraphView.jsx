// src/components/GraphView.jsx
import React, { useRef, useEffect, useCallback } from "react";
import ForceGraph2D from "react-force-graph-2d";

const GraphView = ({ graphData }) => {
  const fgRef = useRef();
  const zoomStep = 0.2;

  // --- Force Adjustments for Sparsity ---
  useEffect(() => {
    if (fgRef.current) {
      // 1. Increase Repulsion (Charge): Larger negative number = more space between nodes
      fgRef.current.d3Force("charge").strength(-400);

      // 2. Increase Link Distance: Pushes connected nodes further apart
      fgRef.current.d3Force("link").distance(150);

      // 3. Adjust Centering: Keeps the sparse graph from drifting off screen
      fgRef.current.d3Force("center").strength(0.1);

      // Reheat the simulation so changes apply immediately
      fgRef.current.d3ReheatSimulation();
    }
  }, [graphData]); // Re-run when data changes (like after a search)

  const handleZoomIn = useCallback(() => {
    if (fgRef.current) {
      const currentZoom = fgRef.current.zoom();
      fgRef.current.zoom(currentZoom * (1 + zoomStep), 200);
    }
  }, []);

  const handleZoomOut = useCallback(() => {
    if (fgRef.current) {
      const currentZoom = fgRef.current.zoom();
      fgRef.current.zoom(currentZoom * (1 - zoomStep), 200);
    }
  }, []);

  const handleRecenter = useCallback(() => {
    if (fgRef.current) {
      fgRef.current.zoomToFit(400, 50);
    }
  }, []);

  const handleScrollLock = useCallback((event) => {
    event.preventDefault();
    event.stopPropagation();
  }, []);

  useEffect(() => {
    const currentRef = fgRef.current;
    if (currentRef && currentRef.el) {
      const canvas = currentRef.el.querySelector('canvas');
      if (canvas) {
        canvas.addEventListener('wheel', handleScrollLock, { passive: false });
        return () => {
          canvas.removeEventListener('wheel', handleScrollLock, { passive: false });
        };
      }
    }
  }, [handleScrollLock]);

  const drawRoundedRect = (ctx, x, y, width, height, radius) => {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
  };

  return (
    <div
      style={{
        border: "1px solid #ccc",
        height: "500px",
        marginTop: "1rem",
        position: 'relative',
        overflow: 'hidden',
        borderRadius: '8px',
        backgroundColor: '#f8fafc' // Subtle background for the canvas
      }}
    >
      {/* Control Buttons */}
      <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 10 }}>
        <button onClick={handleZoomIn} style={buttonStyle}>➕</button>
        <button onClick={handleZoomOut} style={buttonStyle}>➖</button>
        <button onClick={handleRecenter} style={buttonStyle}>🎯</button>
      </div>

      <ForceGraph2D
        ref={fgRef}
        graphData={graphData}

        // --- Physics Decay ---
        d3VelocityDecay={0.3} // Lower means more "slippery" movement

        // --- Link Styling ---
        linkLabel={(link) => `Mode: ${link.relationship || 'Route'}`}
        linkDirectionalArrowLength={3.5}
        linkDirectionalArrowRelPos={1}
        linkCurvature={0.2}
        linkColor={() => '#94a3b8'} // Cleaner gray links

        // --- Node Styling ---
        nodeCanvasObject={(node, ctx, globalScale) => {
          const label = node.name || String(node.id);
          const fontSize = 12 / globalScale;
          ctx.font = `${fontSize}px Inter, Sans-Serif`;
          const textWidth = ctx.measureText(label).width;
          const padding = fontSize * 0.6;
          const bckgDimensions = [textWidth + padding, fontSize + padding];

          const x = node.x - bckgDimensions[0] / 2;
          const y = node.y - bckgDimensions[1] / 2;

          // Background box
          ctx.fillStyle = node.is_match ? '#fff7ed' : 'rgba(255, 255, 255, 0.95)';
          ctx.strokeStyle = node.is_match ? '#f97316' : '#6366f1'; // Highlight matches with Orange
          ctx.lineWidth = (node.is_match ? 2 : 1) / globalScale;

          drawRoundedRect(ctx, x, y, bckgDimensions[0], bckgDimensions[1], 4 / globalScale);
          ctx.fill();
          ctx.stroke();

          // Text
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillStyle = '#1e293b';
          ctx.fillText(label, node.x, node.y);
        }}
        nodePointerAreaPaint={(node, color, ctx) => {
          // Improves click detection for custom nodes
          ctx.fillStyle = color;
          const label = node.name || String(node.id);
          const fontSize = 12;
          const textWidth = ctx.measureText(label).width;
          ctx.fillRect(node.x - textWidth / 2, node.y - fontSize / 2, textWidth, fontSize);
        }}
      />
    </div>
  );
};

const buttonStyle = {
  marginRight: '5px',
  padding: '5px 10px',
  cursor: 'pointer',
  backgroundColor: '#fff',
  border: '1px solid #e2e8f0',
  borderRadius: '4px',
  boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
  fontSize: '14px'
};

export default GraphView;