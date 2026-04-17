import { MessageItem } from '@/contexts/node-context';
import type { BuiltInNode, Node } from '@xyflow/react';

export type NodeMessage = MessageItem;

export type AgentNode = Node<{ name: string, description: string, status: string }, 'agent-node'>;
export type JsonOutputNode = Node<{ name: string, description: string, status: string }, 'json-output-node'>;
export type TradeInputNode = Node<{ name: string, description: string, status: string }, 'portfolio-start-node'>;
export type TradeDecisionNode = Node<{ name: string, description: string, status: string }, 'portfolio-manager-node'>;
export type ProductInputNode = Node<{ name: string, description: string, status: string }, 'stock-analyzer-node'>;

// Legacy aliases for existing components.
export type InvestmentReportNode = JsonOutputNode;
export type PortfolioStartNode = TradeInputNode;
export type PortfolioManagerNode = TradeDecisionNode;
export type StockAnalyzerNode = ProductInputNode;

export type AppNode = BuiltInNode | AgentNode | JsonOutputNode | TradeInputNode | TradeDecisionNode | ProductInputNode;
