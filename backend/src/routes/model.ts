import { Router } from "express";
import ModelController from "../controllers/ModelController";

const router = Router();
const ModelCtl = new ModelController();

// api 리스트
router.get('/list', ModelCtl.getApiList);
// api 학습 상태
router.get('/percent', ModelCtl.getApiLearningPercent);

// api 삭제
router.delete('/api', ModelCtl.delApi);

export default router;