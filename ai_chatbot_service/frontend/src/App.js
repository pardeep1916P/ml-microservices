
import React, {useState} from "react";

export default function App(){
  const [res, setRes] = useState("");
  const call = async () => {
    try{
      const r = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({})
      });
      const j = await r.json();
      setRes(JSON.stringify(j));
    }catch(e){
      setRes("Error: "+e.message);
    }
  }
  return (<div style={{fontFamily:"Arial", padding:20}}>
    <h3>Placeholder frontend for ai_chatbot_service</h3>
    <button onClick={call}>Call backend /predict</button>
    <pre>{res}</pre>
  </div>);
}
