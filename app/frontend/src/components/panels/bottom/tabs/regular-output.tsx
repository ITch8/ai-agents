import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableRow } from '@/components/ui/table';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { cn } from '@/lib/utils';
import { useEffect, useState } from 'react';
import { getDisplayName, getStatusIcon } from './output-tab-utils';
import { ReasoningContent } from './reasoning-content';

// Progress Section Component
function ProgressSection({ sortedAgents }: { sortedAgents: [string, any][] }) {
  if (sortedAgents.length === 0) return null;

  return (
    <Card className="bg-transparent mb-4">
      <CardHeader>
        <CardTitle className="text-lg">Progress</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-1">
          {sortedAgents.map(([agentId, data]) => {
            const { icon: StatusIcon, color } = getStatusIcon(data.status);
            const displayName = getDisplayName(agentId);
            
            return (
              <div key={agentId} className="flex items-center gap-2">
                <StatusIcon className={cn("h-4 w-4 flex-shrink-0", color)} />
                <span className="font-medium">{displayName}</span>
                {data.ticker && (
                  <span>[{data.ticker}]</span>
                )}
                <span className={cn("flex-1", color)}>
                  {data.message || data.status}
                </span>
                {data.timestamp && (
                  <span className="text-muted-foreground text-xs">
                    {new Date(data.timestamp).toLocaleTimeString()}
                  </span>
                )}
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

// Summary Section Component
function SummarySection({ outputData }: { outputData: any }) {
  if (!outputData || !outputData.final_decision) return null;
  const decision = outputData.final_decision;

  return (
    <Card className="bg-transparent mb-4">
      <CardHeader>
        <CardTitle className="text-lg">Final Recommendation</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableBody>
            <TableRow>
              <TableCell className="font-medium">Decision</TableCell>
              <TableCell>{decision.final_decision || '-'}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell className="font-medium">Confidence</TableCell>
              <TableCell>{typeof decision.confidence === 'number' ? `${(decision.confidence * 100).toFixed(1)}%` : '-'}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell className="font-medium">Biggest Risk</TableCell>
              <TableCell>{decision.biggest_risk || '-'}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}

// Analysis Results Section Component
function AnalysisResultsSection({ outputData }: { outputData: any }) {
  const [selectedAgent, setSelectedAgent] = useState<string>('');
  const agents = outputData?.agent_outputs ? Object.keys(outputData.agent_outputs).filter((k: string) => k !== 'trade_decision_agent') : [];

  useEffect(() => {
    if (agents.length > 0 && !selectedAgent) {
      setSelectedAgent(agents[0]);
    }
  }, [agents, selectedAgent]);

  if (!outputData || agents.length === 0) return null;

  return (
    <Card className="bg-transparent">
      <CardHeader>
        <CardTitle className="text-lg">Agent Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs value={selectedAgent} onValueChange={setSelectedAgent} className="w-full">
          <TabsList className="flex space-x-1 bg-muted p-1 rounded-lg mb-4">
            {agents.map((agent) => (
              <TabsTrigger 
                key={agent} 
                value={agent} 
                className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 text-sm font-medium rounded-md transition-colors data-[state=active]:active-bg data-[state=active]:text-blue-500 data-[state=active]:shadow-sm text-primary hover:text-primary hover-bg"
              >
                {getDisplayName(agent)}
              </TabsTrigger>
            ))}
          </TabsList>

          {agents.map((agent) => {
            const analysis = outputData.agent_outputs?.[agent] || {};
            return (
              <TabsContent key={agent} value={agent} className="space-y-4">
                <Table>
                  <TableBody>
                    <TableRow>
                      <TableCell className="font-medium">Confidence</TableCell>
                      <TableCell>{typeof analysis.confidence === 'number' ? `${(analysis.confidence * 100).toFixed(1)}%` : '-'}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell className="font-medium">Details</TableCell>
                      <TableCell className="max-w-3xl">
                        <ReasoningContent content={analysis} />
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TabsContent>
            );
          })}
        </Tabs>
      </CardContent>
    </Card>
  );
}

// Main component for regular output
export function RegularOutput({ 
  sortedAgents, 
  outputData 
}: { 
  sortedAgents: [string, any][]; 
  outputData: any; 
}) {
  return (
    <>
      <ProgressSection sortedAgents={sortedAgents} />
      <SummarySection outputData={outputData} />
      <AnalysisResultsSection outputData={outputData} />
    </>
  );
} 