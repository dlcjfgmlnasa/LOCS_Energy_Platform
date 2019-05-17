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


const BROKEN: string = "BROKEN";
const POWER: string = "POWER";
type verificationTarget = "PHONE" | "EMAIL";

@Entity()
export class Model extends BaseEntity{
  /* primary Key */
  @PrimaryGeneratedColumn("increment") id: number;

  /* 모델 종류 (Broken, Power) */
  @Column({ type: "text", enum: [BROKEN, POWER] })
  target: verificationTarget;

  /* 모델 저장 위치 */
  @Column({ "type": "string" })
  filepath: string;

  /* Building Info (빌딩 데이터 정보) */
  @ManyToOne(type => Building, Building => Building.models)
  building: Building;

  @CreateDateColumn() createdAt: string;
  @UpdateDateColumn() updatedAt: string;
}

export default Model;