import React, { useEffect, useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import routes from '../../constants/routes.json';
import { Col, Container, Row } from 'react-bootstrap';
import ReactImageAnnotate from 'react-image-annotate';
import styles from './AnnotsPage.css';


export default function AnnotsPage(): JSX.Element {
  const [file, setFile] = useState(null as any);
  const history = useHistory();

  function handleExit(state: any) {
    localStorage.setItem("image", JSON.stringify(state.images[0]));
    history.push(routes.DEPENDENCIES);
  }

  useEffect(() => {
    const currentFile = localStorage.getItem('currentFile');
    if (currentFile !== null) {
      setFile(JSON.parse(currentFile));
    }
  }, []);

  return <>
    <Container className={styles.full_screen}>
      <Row>
        <Link to={routes.WELCOME}>Back</Link>
      </Row>
      { file !== null &&
      <ReactImageAnnotate
        labelImages
        regionClsList={["unnamed"]}
        images={[
          {
            src: file.preview,
            name: 'Image',
          }
        ]}
        enabledTools={["select", "create-box"]}

        onExit={handleExit}
      /> }
    </Container>
  </>;
}
