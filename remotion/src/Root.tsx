import { Composition } from "remotion";
import { TickEngine } from "./TickEngine";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="TickEngine"
        component={TickEngine}
        durationInFrames={210}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{}}
      />
    </>
  );
};
