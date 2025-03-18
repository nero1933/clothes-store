import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/api/v1/products/')
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error('Error while fetching data', error);
      });
  }, []);

  return (
    <div>

      <h1>Data from API:</h1>

      {data ? (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default App;