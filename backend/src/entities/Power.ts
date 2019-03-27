import {
  BaseEntity,
  Entity,
  Column,
  CreateDateColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
  UpdateDateColumn
} from "typeorm"
import building from "./Building";


@Entity()
class Power extends BaseEntity{
  /* primary Key */
  @PrimaryGeneratedColumn() id: number;

  /* year (년도) */
  @Column({ "type": "int" })
  year: number;

  /* month (달) */
  @Column({ "type": "int" })
  month: number;

  /* day (일) */
  @Column({ "type": "int" })
  day: number;

  /* hour (시간) */
  @Column({ "type": "int" })
  hour: number;

  /* minute (분) */
  @Column({ "type": "int" })
  minute: number;

  /* Building Info (빌딩 데이터 정보) */
  @ManyToOne(type => building, building => building.powers)
  building: building[];

  @CreateDateColumn() createdAt: string;
  @UpdateDateColumn() updatedAt: string;

}

export default Power;