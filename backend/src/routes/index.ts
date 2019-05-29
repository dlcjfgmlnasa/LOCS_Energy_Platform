import { Router } from "express";
import building from "./building";
import power from "./power";
import model from "./model";

const routes = Router();

routes.use('/building', building);
routes.use('/power', power);
routes.use('/model', model);

export default routes;