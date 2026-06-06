import { C1Chat } from "@thesysai/genui-sdk";
import "@crayonai/react-ui/styles/index.css";
import { themePresets } from "@crayonai/react-ui";

function App() {
  return (
    <div style={{ height: "100vh" }}>
      {/* Chiamata al backend tramite nome servizio Docker */}
      <C1Chat 
        apiUrl="http://localhost:8000/chat" 
        theme={{ ...themePresets.jade, mode: "dark" }}/>
    </div>
  );
}

export default App;



