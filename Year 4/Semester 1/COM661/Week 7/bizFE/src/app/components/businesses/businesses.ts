import { Component } from '@angular/core';
import { BusinessData } from '../../services/business-data';

@Component({
  imports: [],
  providers: [BusinessData],
  selector: 'app-businesses',
  styleUrl: './businesses.css',
  templateUrl: './businesses.html',
})
export class Businesses {

  constructor(protected businessData: BusinessData){}

  business_list: any[] = [];
  page:number = 1;  // page num default

  ngOnInit() {
    if (sessionStorage['page']) {
      this.page = Number(sessionStorage['page'])
    }
    this.business_list = this.businessData.getBusinesses(this.page);
  }

  previousPage() {
    if (this.page > 1) {
      this.page = this.page - 1;
      sessionStorage['page'] = this.page.toString();
      this.business_list = this.businessData.getBusinesses(this.page);
    }
  }
  nextPage() {
    if (this.page < this.businessData.getLastPageNumber()) {
      this.page = this.page + 1;
      sessionStorage['page'] = this.page.toString();
      this.business_list = this.businessData.getBusinesses(this.page);
    }
  }
}
