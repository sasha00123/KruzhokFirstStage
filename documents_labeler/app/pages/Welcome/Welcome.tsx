import React, { useEffect, useState } from 'react';

import { useDropzone } from 'react-dropzone';
import { Col, Container, Row } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import routes from '../../constants/routes.json';
import styles from './Welcome.css';
import logo from './logo.png';

const thumb = {
  borderRadius: 2,
  marginBottom: 8,
  marginRight: 8,
  width: 100,
  height: 100,
  padding: 4,
  boxSizing: 'border-box'
};


const img = {
  width: 'auto',
  height: '100%'
};

export default function Welcome(): JSX.Element {
  const [file, setFile] = useState(null as any);
  const { getRootProps, getInputProps } = useDropzone({
    accept: 'image/*',
    multiple: false,
    onDrop: acceptedFiles => {
      setFile(Object.assign(acceptedFiles[0], {
        preview: URL.createObjectURL(acceptedFiles[0])
      }));
    }
  });

  useEffect(() => {
    if (file !== null) {
      localStorage.setItem('currentFile', JSON.stringify(file));
    }
  }, [file]);

  // useEffect(() => () => {
  //   // Make sure to revoke the data uris to avoid memory leaks
  //   if (file !== null) {
  //     URL.revokeObjectURL(file.preview);
  //   }
  // }, [file]);

  return (
    <Container>
      <Row className={`${styles.full_screen} `}>
        <Col className='d-flex'>
          <div className='mx-auto my-auto'>
            <Row className='m-5'>
              <img src={logo} alt="logo" className={`${styles.logo} mx-auto`}/>
            </Row>
            <Row className='m-5'>
              <div {...getRootProps({ className: `${styles.dropzone} mx-auto` })}>
                <input {...getInputProps()} />
                <p>Перетащите файл для разметки сюда, или нажмите, чтобы выбрать.</p>
              </div>
            </Row>
            {file !== null &&
            <>
              <Row>
                <Col style={thumb} key={file.name} className='text-center'>
                  <img
                    src={file.preview}
                    style={img}
                  />
                </Col>
              </Row>
              <Row>
                <Col className="text-center">
                  <Link to={routes.ANNOTATIONS}>
                    Выбрать
                  </Link>
                </Col>
              </Row>
            </>
            }
          </div>
        </Col>
      </Row>
    </Container>
  );
}
