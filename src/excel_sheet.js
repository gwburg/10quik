import { useEffect } from 'react';
import Source from './source.js'

export default function ExcelSheet(props) {
  useEffect(() => {
    const script = document.createElement('script');

    script.src = Source.onedrive;
    console.log(Source.onedrive);
    script.async = true;

    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    }
  });

  return (
    <div id="myExcelDiv" frameborder="0" style={{width: "1000px", height: "1000px"}}></div>
  );
}
