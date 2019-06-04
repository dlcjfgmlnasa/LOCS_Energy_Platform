import { Request, Response } from "express";
import { getRepository, getConnection } from "typeorm";
import { Model } from "../entities/Model";


/* Building Model (Build.ts) Controller */
class ModelController {
  // api 리스트
  public getApiList = async (req: Request, res: Response) => {
    try{
      const list = await getRepository(Model)
      .createQueryBuilder("model")
      .leftJoinAndSelect("model.building", "building")
      .where("model.api_status = :api_status", { api_status: req.param('api_status')})
      .getMany();

      res.json(list);
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }

  // api 리스트
  public getNewApiList = async (req: Request, res: Response) => {
    try{
      const list = await getRepository(Model)
      .createQueryBuilder("model")
      .orderBy("model.updatedAt", "DESC")
      .limit(5)
      .getMany();

      res.json(list);
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }

  // 학습 퍼센트, 로그 출력
  public getApiLearningPercent = async (req: Request, res: Response) => {
    try{
      const list = await getRepository(Model)
      .createQueryBuilder("model")
      .select("model.learning_percent")
      .addSelect("model.learning_log")
      .addSelect("model.target")
      .where("model.buildingId = :id AND model.target = :target", { id: req.param('id'), target: req.param('target') })
      .getMany();

      res.json(list);
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }

  // api 삭제
  public delApi = async (req: Request, res: Response) => {
    try{
      await getConnection()
      .createQueryBuilder()
      .delete()
      .from(Model)
      .where("id = :id", { id: req.param('id')})
      .execute();
      res.json({ status: 'ok' });
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }
}

export default ModelController;