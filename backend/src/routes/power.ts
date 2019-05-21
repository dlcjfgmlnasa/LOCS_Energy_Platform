import { Router } from "express";
import PowerController from "../controllers/PowerController";

const router = Router();
const powerCnt = new PowerController();
router.get('/energy/minute', powerCnt.getEngMinute);
router.get('/energy/hour', powerCnt.getEngHour);
router.get('/energy/day', powerCnt.getEngDay);
router.get('/energy/month', powerCnt.getEngMonth);

export default router;