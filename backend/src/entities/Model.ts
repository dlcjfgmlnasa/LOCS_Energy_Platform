import {
  BaseEntity,
  Entity,
  Column,
  CreateDateColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
  UpdateDateColumn
} from "typeorm"
import { Building } from "./Building";

type MODEL_TYPE = "BROKEN" | "POWER";
type LEANING_STATUS = "STOP" | "LEARNING" | "COMPLETE" | "FAILURE";

@Entity()
export class Model extends BaseEntity{
  /* primary Key */
  @PrimaryGeneratedColumn("increment") id: number;

  /* api_key (api_key) */
  @Column({ type: "varchar", length: 100 })
  api_key: string;

  /* 모델 이름 (filename) */
  @Column({ type: "varchar", length: 100 })
  filename: string;

  /* 모델 저장 위치 (filepath) */
  @Column({ type: "varchar", length: 200 })
  filepath: string;

  /* learning percent */
  @Column({ type: "float", nullable: true})
  learning_percent: number;

  /* learning log */ 
  @Column({ type: "varchar", length: 200, nullable: true})
  learning_log: string;

  /* learning status */
  @Column({ type: "enum", enum: ["STOP", "LEARNING", "COMPLETE", "FAILURE"], default: "STOP"})
  learning_status: LEANING_STATUS;

  /* 모델 종류 [Broken, Power] */
  @Column({ type: "enum", enum: ["BROKEN", "POWER"] })
  target: MODEL_TYPE;

  /* Building Info (빌딩 데이터 정보) */
  @ManyToOne(type => Building, Building => Building.models)
  building: Building;

  @CreateDateColumn() createdAt: string;
  @UpdateDateColumn() updatedAt: string;
}

export default Model;
