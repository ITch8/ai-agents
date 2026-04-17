import { Edge, type NodeTypes } from '@xyflow/react';

import { AgentNode } from './components/agent-node';
import { JsonOutputNode } from './components/json-output-node';
import { PortfolioManagerNode } from './components/portfolio-manager-node';
import { PortfolioStartNode } from './components/portfolio-start-node';
import { StockAnalyzerNode } from './components/stock-analyzer-node';
import { type AppNode } from './types';

// Types
export * from './types';

export const initialNodes: AppNode[] = [
  {
    id: 'stock-analyzer-node',
    type: 'stock-analyzer-node',
    position: { x: 0, y: 0 },
    data: {
      name: 'Trade Question Input',
      description: 'Enter foreign-trade product or market question',
      status: 'Idle',
    },
  },
  {
    id: 'market_agent',
    type: 'agent-node',
    position: { x: 320, y: 25 },
    data: {
      name: 'Market Agent',
      description: 'Market opportunity specialist',
      status: 'Idle',
    },
  },
  {
    id: 'customer_agent',
    type: 'agent-node',
    position: { x: 320, y: 150 },
    data: {
      name: 'Customer Agent',
      description: 'Customer acquisition specialist',
      status: 'Idle',
    },
  },
  {
    id: 'trade_decision-node',
    type: 'portfolio-manager-node',
    position: { x: 640, y: 95 },
    data: {
      name: 'Decision Node',
      description: 'Final trade decision maker',
      status: 'Idle',
    },
  },
];

export const initialEdges: Edge[] = [
  { id: 'e1', source: 'stock-analyzer-node', target: 'market_agent' },
  { id: 'e2', source: 'stock-analyzer-node', target: 'customer_agent' },
  { id: 'e3', source: 'market_agent', target: 'trade_decision-node' },
  { id: 'e4', source: 'customer_agent', target: 'trade_decision-node' },
];

export const nodeTypes = {
  'agent-node': AgentNode,
  'json-output-node': JsonOutputNode,
  'portfolio-start-node': PortfolioStartNode,
  'portfolio-manager-node': PortfolioManagerNode,
  'stock-analyzer-node': StockAnalyzerNode,
} satisfies NodeTypes;
