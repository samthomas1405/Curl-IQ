'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/lib/auth';

export function Navigation() {
  const { logout } = useAuth();

  return (
    <nav className="bg-[#FFF9F5] border-b border-[#D4A574]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/dashboard" className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
              <Image
                src="/logo.png"
                alt="CurlLabs Logo"
                width={60}
                height={60}
                className="object-contain"
                unoptimized
              />
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/dashboard">
              <Button variant="ghost" className="text-[#6B6B6B] hover:text-[#1A1A1A]">Dashboard</Button>
            </Link>
            <Link href="/products">
              <Button variant="ghost" className="text-[#6B6B6B] hover:text-[#1A1A1A]">Products</Button>
            </Link>
            <Link href="/routines">
              <Button variant="ghost" className="text-[#6B6B6B] hover:text-[#1A1A1A]">Routines</Button>
            </Link>
            <Link href="/logs">
              <Button variant="ghost" className="text-[#6B6B6B] hover:text-[#1A1A1A]">Logs</Button>
            </Link>
            <Link href="/profile">
              <Button variant="ghost" className="text-[#6B6B6B] hover:text-[#1A1A1A]">Profile</Button>
            </Link>
            <Button variant="ghost" onClick={logout} className="text-[#6B6B6B] hover:text-[#1A1A1A]">
              Logout
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}
