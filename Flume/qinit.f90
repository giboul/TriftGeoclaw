subroutine qinit(meqn,mbc,mx,xlower,dx,q,maux,aux)

    ! Set initial conditions for the q array.

    use geoclaw_module, only: sea_level
    use grid_module, only: xcell

    ! uncomment if any of these needed...
    use geoclaw_module, only: dry_tolerance, grav

    implicit none

    integer, intent(in) :: meqn,mbc,mx,maux
    real(kind=8), intent(in) :: xlower,dx
    real(kind=8), intent(in) :: aux(maux,1-mbc:mx+mbc)
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc)

    !locals
    integer :: i
    real(kind=8) :: x0,width,eta,x

    x0 = -10.d3   ! initial location of step

    do i=1,mx
      x = xlower +(i-0.5)*dx
      q(1,i) = 0.
      if (x >=-100 .and. x<=0) then
         q(1,i) = 1.d0
      else if (x > 50 .and. 100 > x) then
         q(1,i) = 5.d0/100*(x-50)
      else if (x >= 100) then
         q(1,i) = 5.d0/100*(100-50)
      endif	  
      q(2,i) = 0.  ! right-going
    end do


end subroutine qinit
