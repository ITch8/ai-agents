import { useFlowContext } from '@/contexts/flow-context';
import { useNodeContext } from '@/contexts/node-context';
import { cn } from '@/lib/utils';
import { useEffect, useState } from 'react';
import { sortAgents } from './output-tab-utils';
import { RegularOutput } from './regular-output';

interface OutputTabProps {
  className?: string;
}

export function OutputTab({ className }: OutputTabProps) {
  const { currentFlowId } = useFlowContext();
  const { getAgentNodeDataForFlow, getOutputNodeDataForFlow } = useNodeContext();
  const [updateTrigger, setUpdateTrigger] = useState(0);
  
  // Get current flow data
  const agentData = getAgentNodeDataForFlow(currentFlowId?.toString() || null);
  const outputData = getOutputNodeDataForFlow(currentFlowId?.toString() || null);
  
  // Force re-render periodically to show real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setUpdateTrigger(prev => prev + 1);
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);
  
  // Sort agents for display
  const sortedAgents = sortAgents(Object.entries(agentData));
  
  return (
    <div className={cn("h-full overflow-y-auto font-mono text-sm", className)}>
      <RegularOutput sortedAgents={sortedAgents} outputData={outputData} />
      
      {/* Empty State */}
      {!outputData && sortedAgents.length === 0 && (
        <div className="text-center py-8 text-muted-foreground">
          No output to display. Run a trade decision to see progress and results.
        </div>
      )}
    </div>
  );
} 