import { Router } from "express";
import BuildingController from "../controllers/BuildingController";

const router = Router();
const bldCnt = new BuildingController();

router.get('/list', bldCnt.getBldList);
router.get('/broken/list', bldCnt.getBldBrokenList);

export default router;