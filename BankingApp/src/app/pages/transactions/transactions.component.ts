import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import{Location} from '@angular/common';
import { AuthService } from '../service/auth.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-transactions',
  templateUrl: './transactions.component.html',
  styleUrls: ['./transactions.component.css'],
  imports:[CommonModule,FormsModule],
  standalone: true,
})
export class TransactionsComponent implements OnInit {
  transactions: any[] = [];

  constructor(private loaction:Location,private authService:AuthService, private router:Router) { }
  goBack():void{
    this.loaction.back();
  }
  ngOnInit(): void {
    this.transactions = this.generateMockTransactions(10); // Change the number as per your requirement
  }

  // make_transaction(data:any){
  //   const amount=data.amount;
  //   this.authService.Make_transaction(amount).subscribe(
  //     response => {
  //       console.log('Transaction successful:', response);
  //       this.router.navigateByUrl('/dashboard');
  //     },
  //     error => {
  //       console.error('Transaction failed: ', error);
  //     }
  //   );
  // }

  generateMockTransactions(numTransactions: number): any[] {
    const transactions = [];
    for (let i = 1; i <= numTransactions; i++) {
      transactions.push({
        transactionId: i,
        amount: this.getRandomAmount(),
        date: this.getRandomDate(),
        type: this.getRandomType(),
        account: this.getRandomAccount()
      });
    }
    return transactions;
  }

  getRandomAmount(): number {
    return Math.floor(Math.random() * 1000); // Random amount between 0 and 999
  }

  getRandomDate(): string {
    const year = Math.floor(Math.random() * 10) + 2010; // Random year between 2010 and 2019
    const month = Math.floor(Math.random() * 12) + 1; // Random month between 1 and 12
    const day = Math.floor(Math.random() * 28) + 1; // Random day between 1 and 28 (for simplicity)
    return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
  }

  getRandomType(): string {
    const types = ['Credit', 'Debit'];
    return types[Math.floor(Math.random() * types.length)];
  }

  getRandomAccount(): string {
    const accounts = ['Savings', 'Checking'];
    return accounts[Math.floor(Math.random() * accounts.length)];
  }
}
