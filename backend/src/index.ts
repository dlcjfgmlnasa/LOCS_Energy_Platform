import express from "express";
import dotenv from "dotenv";
import connectionOptions from "./ormConfig";
import { createConnection } from "typeorm";
import helmet from "helmet";
import cors from "cors";
import bodyParser from "body-parser";

dotenv.config();

// jsonwebtoken - Will handle the jwt operations for us
// bcryptjs - Help us to hash user passwords
// typeorm - The ORM we are going to use to manipulate database
// reflect-metadata - allow some annotations features used with TypeORM
// class-validator - A validation package that works really well with TypeORM
// ts-node-dev - Automatically restarts the server when we change any file

createConnection(connectionOptions)
  .then(() => {
    // Create a new express application instance
    const app = express();

    // Call Middleware
    app.use(cors());                    /* cors - Enable cross-origin Requests */
    app.use(helmet());                  /* helmet - Help us to secure our application by setting various HTTP headers */
    app.use(bodyParser.json());         /* body-parser - Parses the client’s request from json into javascript objects */

    app.listen(Number(process.env.HOST_PORT), String(process.env.HOST_DOMAIN), () => {
      console.log(`app listening on http://${process.env.HOST_DOMAIN}:${process.env.HOST_PORT}`);
    });
  })
  .catch(error => console.log(error));