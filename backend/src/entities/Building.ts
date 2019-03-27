import {
  BaseEntity,
  Column,
  CreateDateColumn,
  Entity,
  PrimaryGeneratedColumn,
  OneToMany,
  UpdateDateColumn
} from "typeorm";
import power from "./Power";


@Entity()
class Building extends BaseEntity{
  /* primary Key */
  @PrimaryGeneratedColumn() id: number;

  /* building comment (설명) */
  @Column({ type: "text" , nullable: true })
  comment: string;

  /* building latitude (위도) */
  @Column({ type: "double precision", default: 0 })
  lat: number;

  /* building longitude (경도) */
  @Column({ type: "double precision", default: 0 })
  lng: number;

  /* Power Info (전력 데이터 정보) */
  @OneToMany(type => power, power => power.building)
  powers: power[];

  @CreateDateColumn() createdAt: string;
  @UpdateDateColumn() updatedAt: string;


}

  export default Building;