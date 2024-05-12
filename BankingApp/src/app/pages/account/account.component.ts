import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../service/auth.service'
import { AccountService } from '../../service/acc.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-account',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent {
  accStatus!: string;
  accounts: Account[] = []

  constructor(private authService: AuthService, private accountService: AccountService, private router: Router) { }
  
  ngOnInit(): void {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login']); // Redirect to login if not logged in
    }
    console.log(this.authService.isLoggedIn());
    this.loadAccounts();
  }

  loadAccounts() {
    this.accountService.getMyAccounts().subscribe(
      (response: string) => {
        const jsonResponse = JSON.parse(response); // Parse the JSON string
        this.accounts = jsonResponse as Account[]; // Map the parsed data into the accounts array
        console.log(this.accounts);
      },
      (error) => {
        console.error('Error fetching accounts:', error);
        this.accStatus = error;
      }
    );
  }

  changeAccountStatus(account: Account) {
    const acc_number = account.AccountNumber;
    const acc_status = account.newStatus;
    account.AccStatus = acc_status;
    this.accountService.changeStauts(acc_number, acc_status).subscribe(
      (response: string) => {
        console.log(response);
      },
      (error) => {
        console.error('Error changing status:', error);
      }
    );
  }
}

export interface Account {
  AccountNumber: number,
  AccountType: string,
  AccStatus?: string,
  newStatus?: string
}
