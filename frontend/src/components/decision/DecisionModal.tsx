import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import type { DecisionPayload } from "@/types/telemetry";

interface DecisionModalProps {
  decision: DecisionPayload | null;
  onSubmit: (optionId: string) => void;
}

export function DecisionModal({ decision, onSubmit }: DecisionModalProps) {
  if (!decision) return null;

  return (
    <Dialog open={true}>
      <DialogContent
        className="sm:max-w-md"
        onInteractOutside={(e) => e.preventDefault()}
        onEscapeKeyDown={(e) => e.preventDefault()}
      >
        <DialogHeader>
          <div className="flex items-center gap-2 mb-1">
            <Badge variant="destructive">Risk {decision.currentRiskScore}</Badge>
          </div>
          <DialogTitle>Security Decision Required</DialogTitle>
          <DialogDescription>{decision.prompt}</DialogDescription>
        </DialogHeader>

        <div className="flex flex-col gap-2 mt-2">
          {decision.options.map((opt) => (
            <Button key={opt.id} variant="outline" onClick={() => onSubmit(opt.id)}>
              {opt.label}
            </Button>
          ))}
        </div>
      </DialogContent>
    </Dialog>
  );
}