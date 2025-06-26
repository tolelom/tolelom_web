// frontend/src/App.jsx
import { useState } from 'react';
import { executeBatch } from './services/api';

function App() {
    const [code, setCode] = useState('');
    const [result, setResult] = useState('');

    const handleExecute = () => {
        executeBatch(code).then(res => {
            setResult(res.data.result);
        });
    };

    return (
        <div>
            <textarea value={code} onChange={(e) => setCode(e.target.value)} />
            <button onClick={handleExecute}>실행</button>
            <pre>{result}</pre>
        </div>
    );
}

export default App
